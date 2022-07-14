#include <iostream>
#include <string>
#include <mutex>
#include <curl/curl.h>
#include <pthread.h>
#include <stdio.h>
#include <fstream>


typedef struct{
	char* url;
	char* file;
} arg;

typedef struct{
	arg* args;
	int num_args;
	int curr;
	std::mutex lock;
} globals;


void* pull_one_url(void* data){
	globals* globs = (globals*) data;


	while(true){
		if(globs->curr == globs->num_args){
			return NULL;
		}

		globs->lock.lock();
		int index = globs->curr++;
		globs->lock.unlock();


		if(globs->curr % 25 == 0){
			std::cout << globs->curr << "/" << globs->num_args << "\n";
		}

		arg a = globs->args[index];

		
		FILE* fp = fopen(a.file, "wb");

		CURL* curl = curl_easy_init();
		curl_easy_setopt(curl, CURLOPT_URL, a.url);
		curl_easy_setopt(curl, CURLOPT_WRITEDATA, fp);
		curl_easy_setopt(curl, CURLOPT_IPRESOLVE, CURL_IPRESOLVE_V4);

		curl_easy_perform(curl);

		curl_easy_cleanup(curl);
		fclose(fp);


	}
}


void run(char**, char**, int, int, int) asm("run");

void run(char** extv, char** files, int extc, int threads, int id){

	arg* args = new arg[extc];

	for(int i = 0; i < extc; i++){
		args[i].url = extv[i];
		args[i].file = files[i];
	}

	globals* globs = new globals();
	globs->args = args;
	globs->num_args = extc;
	globs->curr = 0;

	
	pthread_t tid[threads];

	curl_global_init(CURL_GLOBAL_ALL);


	for(int i = 0; i < threads; i++){
		int err = pthread_create(&tid[i], NULL, pull_one_url, (void*)globs);
		if(err){
			std::cout << err;
		}
	}

	for(int i = 0; i < threads; i++){
		pthread_join(tid[i], NULL);
	}

	curl_global_cleanup();

	std::cout << "Finished CURLing. Merging TS Files\n";

	char* ofname = new char[48];
	sprintf(ofname, "dumps/%d.ts", id);

	std::ofstream of(ofname, std::ios_base::binary);
	for(int i = 0; i < extc; i++){
		std::ifstream input_file(files[i], std::ios_base::binary);

		of << input_file.rdbuf();

		input_file.close();
		std::remove(files[i]);
	}


	std::cout << "\n";
}
