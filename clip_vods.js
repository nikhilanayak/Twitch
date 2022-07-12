import {gql, GraphQLClient} from "graphql-request";
import fs from "fs";
import twitch from "twitch-m3u8";
import request from "request";
import ids from "./ids.json" assert {type: "json"};

import chalk from "chalk";
import vodtwitch from "vodtwitch";

import {execSync} from "child_process";


const URL = "https://gql.twitch.tv/gql";

const client = new GraphQLClient(URL, {headers: {
	"Client-ID": "kimne78kx3ncx6brgo4mv6wki5h1ko"
}});






let TID = parseInt(process.argv[2]);
let THREADS = parseInt(process.argv[3]);

function debug(msg){
	console.log(`THREAD [${TID}] said ${msg}`);
}

//console.log(`Running ${THREADS} threads, I am ${TID}`);

async function getClips(id){
	const query = 
	gql`
	query($id: ID, $cursor: Cursor){
		video(id: $id){
			clips(first: 100, after: $cursor){
				edges{
					node{
						durationSeconds
						videoOffsetSeconds
						viewCount

					}
					cursor
				}
				pageInfo{
					hasNextPage
				}
			}
		}
	}
	`;

	let cursor = "";
	let clips = [];

	let page = 1;

	while(true){
		let data;
		try{
			data = await client.request(query, {id: id, cursor: cursor});
		}
		catch(err){
			//console.error(err);
			continue;
		}
		if(data.video == null){
			break;
		}

		clips.push(...(data.video.clips.edges));

		
		if(!data.video.clips.pageInfo.hasNextPage){
			break;	
		}

		cursor = data.video.clips.edges[data.video.clips.edges.length - 1].cursor;

		//process.stdout.write(`ID: ${id} - Page: ${page++} - Clips: ${clips.length}`);

	}
	return clips;	
}




//TID = parseInt(Math.random() * ids.data.length);

debug("Started");
let num = 0;

for(let i = TID; i < ids.data.length; i += THREADS){
	const id = ids.data[i].node.id;
	const clips = await getClips(id);

	let urls;
	try{
		urls = (await twitch.getVod(id.toString())).filter(i=>i.quality == "Audio Only");
	}
	catch(err){
		debug(chalk.red(`Failed ${id}`));
		continue;
	}

	if(urls.length == 0){
		debug(chalk.red(`Failed ${id}`));
		continue;
	}

	fs.mkdirSync(`data/${id}`);
	fs.writeFileSync(`data/${id}/clips.json`, JSON.stringify({"nc": clips.length, "clips": clips, "url": urls[0], "len": ids.data[i].node.lengthSeconds}));


	debug(`Finished #${num++} (${id}) - ${clips.length} clips - (${parseInt(num / ids.data.length * THREADS * 100 * 100)/100})`);

}

//console.log(JSON.stringify(await getClips(ID)));
