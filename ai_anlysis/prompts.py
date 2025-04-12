from typing import Dict, Any


class GeminiPrompts:
    @staticmethod
    def improve_description_prompt(project_data: Dict[str, Any]) -> str:
        """
        Create a prompt for improving project description
        """
        return f"""
        You are an expert consultant for tech project submissions to a university competition called CodingMaster'2025.
        Below is a project description that needs to be improved:

        PROJECT TITLE: {project_data['title']}
        ORIGINAL DESCRIPTION: {project_data['description']}

        Please provide an improved, more professional version of this description that:
        1. Is clearer and more concise
        2. Highlights the project's key features and benefits
        3. Uses proper technical terminology
        4. Is well-structured with proper paragraphs
        5. Is between 200-300 words

        Return only the improved description without any additional comments or explanations.
        """

    @staticmethod
    def score_idea_prompt(project_data: Dict[str, Any]) -> str:
        """
        Create a prompt for scoring project idea
        """
        return f"""
        You are an expert evaluator for tech project submissions to a university competition called CodingMaster'2025.

        PROJECT TITLE: {project_data['title']}
        PROJECT DESCRIPTION: {project_data['description']}

        Please evaluate this project idea on a scale of 0.0 to 10.0 based on:
        1. Innovation and originality (0-10)
        2. Technical feasibility (0-10)
        3. Market potential (0-10)
        4. Clarity of purpose (0-10)
        5. Overall impact (0-10)

        After evaluating, provide:
        1. A score for each category
        2. A detailed explanation for each score (1-2 sentences each)
        3. A final overall score (average of the five categories, rounded to one decimal place)

        Format your response as a JSON object like this:
        {{
            "innovation_score": 0.0,
            "innovation_explanation": "",
            "feasibility_score": 0.0,
            "feasibility_explanation": "",
            "market_score": 0.0,
            "market_explanation": "",
            "clarity_score": 0.0,
            "clarity_explanation": "",
            "impact_score": 0.0,
            "impact_explanation": "",
            "overall_score": 0.0
        }}

        Return only this JSON object without any additional text.
        """

    @staticmethod
    def suggestions_prompt(project_data: Dict[str, Any]) -> str:
        """
        Create a prompt for providing project suggestions
        """
        return f"""
        You are an expert advisor for tech project submissions to a university competition called CodingMaster'2025.

        PROJECT TITLE: {project_data['title']}
        PROJECT DESCRIPTION: {project_data['description']}

        Please provide constructive suggestions for improving this project in the following areas:
        1. Technical enhancements
        2. Features that could be added
        3. Potential challenges to address
        4. Implementation considerations
        5. Presentation tips for the competition

        For each area, provide 1-2 specific, actionable suggestions.

        Format your response as a JSON object like this:
        {{
            "technical_suggestions": ["", ""],
            "feature_suggestions": ["", ""],
            "challenge_suggestions": ["", ""],
            "implementation_suggestions": ["", ""],
            "presentation_suggestions": ["", ""]
        }}

        Return only this JSON object without any additional text.
        """
