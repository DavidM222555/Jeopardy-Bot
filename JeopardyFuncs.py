import pandas as pd
from typing import Tuple

class JeopardyWrapper:
    def __init__(self):
        self.jeopardy_df = pd.read_csv('assets/JEOPARDY_CSV.csv')


    def get_random_entry(self) -> Tuple[str, str, str, int]:
        question = None 
        answer = None
        value = None

        # Process for filtering out questions that contain external media until 
        # I can find a decent way to display it with the question itself
        while(True):
            random_question = self.jeopardy_df.sample()

            category = random_question['Category'].iloc[0]
            question = random_question['Question'].iloc[0]
            answer = random_question['Answer'].iloc[0]
            value = random_question['Value'].iloc[0]

            if("href" not in question):
                break


        if(value == 'None'): # This means it was a final jeopardy -- handled elsewhere
            value = 0

        return (category, question, answer, value)
    
    

    



        
        

