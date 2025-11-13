from fastapi import Depends

from database.core import get_session
from features.questionnaires.models import QuestionnaireCreate
from features.questionnaires.service import create_questionnaire
from features.questions.service import list_questions

if __name__ == "__main__":


    session = next(get_session())
    questions_read_list = list_questions(session)
    print(f"Questions read: {questions_read_list}")
    questions_list = [question.id for question in questions_read_list]
    
    # print(f"Questions list: {questions_list}")

    questionnaire_create = QuestionnaireCreate(
        title="Sample Questionnaire",
        description="This is a sample questionnaire created for testing purposes.",
        questions=questions_list, 
        )
    questionnaire = create_questionnaire(questionnaire_create, session=session)
    print(f"Questionnaire created with ID: {questionnaire.id}")


