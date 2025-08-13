# assistant/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from openai import OpenAI
from dotenv import load_dotenv
import os
from .models import Question, PetType
from .serializers import QuestionSerializer
from rest_framework import status
import json

client = OpenAI()
# Load environment variables
if os.path.exists("/etc/secrets/.env"):
    load_dotenv("/etc/secrets/.env")
else:
    load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ChatbotAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_input = request.data.get("message", "").strip()

        if not user_input:
            return Response({"reply": "Please enter a question about dogs or cats."}, status=400)

        if len(user_input) > 500:
            return Response({"reply": "Message too long."}, status=400)

        system_prompt = (
            "You are a helpful veterinarian and animal care expert. "
            "You specialize in all types of pets and animals including exotic ones. "
            "Your job is to provide clear, concise, and useful answers to questions about any pets or animals. "
            "Focus on essential info only—health, training, diet, adoption, care, safety, and behavior. "
            "Avoid long explanations. Limit answers to 2-3 short sentences or quick bullet points. "
            "If steps are needed, list them briefly. "
            "Do not answer anything unrelated to animals or pets."
        )

        try:
            response = client.chat.completions.create(
                model="gpt-4-0613",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ]
            )

            reply = response.choices[0].message.content.strip()
            return Response({"reply": reply})
        except Exception as e:
            return Response({"reply": "Sorry, an error occurred while processing your request."}, status=500)

class PetQuizQuestionsAPIView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        questions = Question.objects.prefetch_related('options__scores').all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)
    
class PetRecommendationAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        answers = request.data.get("answers")
        scores = request.data.get("scores")
        best_pet = request.data.get("bestPet")
        print("answers:", answers)
        print("scores:", scores)
        print("best_pet:", best_pet)

        if not answers or not scores or not best_pet:
            return Response({"error": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)

        prompt = self.build_prompt(answers, scores, best_pet)

        try:
            response = client.chat.completions.create(
                model="gpt-4-0613",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a helpful veterinarian and animal care expert. "
                            "You specialize in all types of pets and animals including exotic ones. "
                            "Your job is to provide clear, concise, and useful answers to questions about any pets or animals. "
                            "Focus on essential info only—health, training, diet, adoption, care, safety, and behavior. "
                            "Avoid long explanations. Limit answers to 2-3 short sentences or quick bullet points. "
                            "If steps are needed, list them briefly. "
                            "Do not answer anything unrelated to animals or pets."
                        ),
                    },
                    {
                        "role": "user",
                        "content": (
                            prompt
                            + "\n\nReturn your response strictly in the following JSON format:\n"
                            + json.dumps({
                                "summary": "Short explanation of why this pet type is best",
                                "top_breeds": [
                                    {"name": "Breed Name", "reason": "Why it fits"},
                                    {"name": "Breed Name", "reason": "Why it fits"},
                                    {"name": "Breed Name", "reason": "Why it fits"},
                                    {"name": "Breed Name", "reason": "Why it fits"},
                                    {"name": "Breed Name", "reason": "Why it fits"}
                                ]
                            }, indent=2)
                        )
                    }
                ],
                temperature=0.7,
                max_tokens=700,
            )

            raw = response.choices[0].message.content.strip()
            print("RAW:", raw)

            # Try to parse JSON response
            try:
                parsed = json.loads(raw)
                return Response(parsed)
            except json.JSONDecodeError:
                return Response({
                    "error": "Failed to parse JSON from OpenAI response.",
                    "raw": raw
                }, status=status.HTTP_502_BAD_GATEWAY)

        except Exception as e:
            return Response(
                {"error": f"OpenAI request failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def build_prompt(self, answers, scores, best_pet):
        score_lines = "\n".join([f"- {k.capitalize()}: {v}" for k, v in scores.items()])
        return (
            f"The user took a pet quiz. Based on their answers, the recommended pet type is: {best_pet.upper()}.\n\n"
            f"Here are the total scores:\n{score_lines}\n\n"
            f"Explain why this pet type was chosen. Also recommend the top 5 most suitable breeds (if applicable), "
            f"based on the user's answers. Include a short reason why each breed is a good fit."
        )
