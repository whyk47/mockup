import json
from typing import Iterable
import google.generativeai as genai
from google.generativeai.types import File
import os
import time
from random import random
from dotenv import load_dotenv

class DataProcessor:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(DataProcessor, cls).__new__(cls)
        return cls.instance
    
    def __init__(self):
        load_dotenv()
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])

        self.generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
            "response_mime_type": "application/json",
        }

        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=self.generation_config,
        )
    
    def __upload_to_gemini(self, path: str, mime_type: str | None = None) -> File:
        """Uploads the given file to Gemini.

        See https://ai.google.dev/gemini-api/docs/prompting_with_media
        """
        file = genai.upload_file(path, mime_type=mime_type)
        print(f"Uploaded file '{file.display_name}' as: {file.uri}")
        return file
    
    def __wait_for_files_active(self, files: Iterable[File]) -> None:
        """Waits for the given files to be active.

        Some files uploaded to the Gemini API need to be processed before they can be
        used as prompt inputs. The status can be seen by querying the file's "state"
        field.

        This implementation uses a simple blocking polling loop. Production code
        should probably employ a more sophisticated approach.
        """
        print("Waiting for file processing...")
        for name in (file.name for file in files):
            file = genai.get_file(name)
            while file.state.name == "PROCESSING":
                print(".", end="", flush=True)
                time.sleep(10)
                file = genai.get_file(name)
                if file.state.name != "ACTIVE":
                    raise Exception(f"File {file.name} failed to process")
        print("...all files ready\n")

    def process(self) -> None:
        files = [
            self.__upload_to_gemini("recruitment/services/scraper/files/scrape.txt", mime_type="text/plain"),
        ]

        with open('recruitment/services/scraper/files/prompt.txt', 'r') as f:
            prompt = f.read()

        # Some files have a processing delay. Wait for them to be ready.
        self.__wait_for_files_active(files)

        print("Generating content...")
        response = self.model.generate_content([prompt, *files])
        with open('recruitment/services/scraper/files/response.txt', 'w') as f:
            f.write(response.text)

        response = list(json.loads(response.text).values())[0]

        with open('recruitment/services/scraper/files/scrape.json', 'r') as f:
            jobs = json.load(f)

        if len(jobs) != len(response):
            raise Exception("Number of jobs does not match number of responses")
        for i in range(len(jobs)):
            jobs[i] = {**jobs[i], **response[i]}
            jobs[i]['mandatory_skill_list'] = ''.join(jobs[i]['Mandatory Skill(s)'])
            jobs[i]['desirable_skill_list'] = ''.join(jobs[i]['Desirable Skill(s)'])
            jobs[i]['responsibility_list'] = ''.join(jobs[i]['Responsibilities'])
            for key in ['id', 'Mandatory Skill(s)', 'Desirable Skill(s)', 'Responsibilities']:
                jobs[i].pop(key)

        with open('recruitment/services/scraper/files/jobs.json', 'w') as f:
            json.dump(jobs, f, indent=4)

        print("Saved to jobs.json")

if __name__ == '__main__':
    data_processor = DataProcessor()
    data_processor.process()



