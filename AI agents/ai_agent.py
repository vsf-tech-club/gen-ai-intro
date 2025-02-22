import os
import google.generativeai as genai
from dotenv import load_dotenv

class GeminiService:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError('GEMINI_API_KEY environment variable is not set')
        
        genai.configure(api_key=api_key)
        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
        }
        
        self.model = genai.GenerativeModel(
            model_name="gemini-2.0-flash-exp",
            generation_config=generation_config
        )
    
    async def generate_content(self, prompt):
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as error:
            print('Error generating content:', error)
            raise error

class AIAgent:
    def __init__(self):
        self.gemini_service = GeminiService()
        self.memory = {
            'conversation_history': [],
            'task_history': [],
            'learnings': {}
        }
        self.current_task = None
    
    async def execute_task(self, task):
        try:
            self.current_task = task
            
            # Analyze task and break it down
            task_analysis = await self.analyze_task(task)
            
            # Store in memory
            self.memory['task_history'].append({
                'task': task,
                'analysis': task_analysis
            })

            # Generate and execute plan
            response = await self.generate_and_execute_plan(task_analysis)
            
            # Learn from execution
            await self.learn_from_execution(task, response)
            
            return response
        except Exception as error:
            print('Error executing task:', error)
            self.memory['learnings'][f'error_{len(self.memory["learnings"])}'] = {
                'task': task,
                'error': str(error)
            }
            raise error
    
    async def analyze_task(self, task):
        analysis_prompt = f"""Analyze this task and break it down into steps:
        Task: {task}
        Consider:
        1. What are the main components of this task?
        2. What knowledge is required?
        3. What potential challenges might arise?
        Please provide a structured analysis."""
        
        return await self.gemini_service.generate_content(analysis_prompt)
    
    async def generate_and_execute_plan(self, analysis):
        plan_prompt = f"""Based on this analysis: {analysis}
        Create a step-by-step plan to accomplish the task.
        Include necessary validations or error checks."""
        
        plan = await self.gemini_service.generate_content(plan_prompt)
        
        # Execute plan with original task context
        return await self.gemini_service.generate_content(
            f"{plan}\n\nNow, execute this plan for: {self.current_task}"
        )
    
    async def learn_from_execution(self, task, result):
        # Store successful patterns
        self.memory['learnings'][f'success_{len(self.memory["learnings"])}'] = {
            'task': task,
            'result': result
        }
        
        # Update conversation history
        self.memory['conversation_history'].extend([
            {'role': 'user', 'content': task},
            {'role': 'assistant', 'content': result}
        ])