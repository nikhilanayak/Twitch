import { request, gql, GraphQLClient} from "graphql-request";
import fs from "fs";
/*const graphql_request = require("graphql-request");
const request = graphql_request.request;
const gql = graphql_request.gql;
const GraphQLClient = graphql_request.GraphQLClient;*/
import categories from "./categories.json" assert {type: "json"};


const URL = "https://gql.twitch.tv/gql";

const client = new GraphQLClient(URL, {headers: {
	"Client-ID": "kimne78kx3ncx6brgo4mv6wki5h1ko"
}});



async function getIDs(categories, minViews){
	const query = 
	gql`
	query($cat: String!, $cursor: Cursor){
		game(name: $cat){
			videos(sort: VIEWS, after: $cursor, first: 500){
				edges{
					node{
						id
						viewCount
						lengthSeconds
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

	const out = [];

	let catnum = 1;
	for(let cat of categories){
		let ids = [];
		let cursor = "";

		let page = 0;

		while(true){
			let data;
			try{
				data = await client.request(query, {cat: cat, cursor: cursor});

			}
			catch(err){
				//console.error(err);
				continue;

			}

			if(data.game == null){
				console.log(`\nSkipped: ${cat}`);
				break;	
			}

			out.push(...(data.game.videos.edges));


			if(!data.game.videos.pageInfo.hasNextPage){
				break;
			}

			let viewCount = data.game.videos.edges[data.game.videos.edges.length - 1].node.viewCount;

			cursor = data.game.videos.edges[data.game.videos.edges.length - 1].cursor;

			process.stdout.write(`(${catnum}/${categories.length}) Category: ${cat} - Page: ${page++} - View Count: ${viewCount} > ${minViews} - Cursor: ${cursor}\r`);
			if(viewCount < minViews){
				break;
			}

		}

		//out[cat] = ids;
		console.log();
		catnum++;

	}

	return out;



}

/*const categories = [
	"Rust",
	"Just Chatting",
	"VALORANT",
	"Fall Guys",
	"Apex Legends",
	"League Of Legends",
	"Fortnite",
	"Escape From Tarkov",
	"Minecraft",
	"Call of Duty: Warzone",
	"Grand Theft Auto V",
	"Dead by Daylight",
	"Counter Strike: Global Offense",
	"World of Warcraft",
	"Rocket League",
	"Monopoly Plus",
	"DOTA 2",
	"Teamfight Tactics"
];*/

//categories = JSON.parse("");

const data = await getIDs([categories[0]], 15000);

fs.writeFileSync("ids.json", JSON.stringify({"data": data}));

console.log(`Finished! Wrote ${data.length} files`);
