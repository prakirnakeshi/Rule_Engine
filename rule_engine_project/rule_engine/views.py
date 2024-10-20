from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, render
import json
import re
from .models import Rule
from .rule_engine import parse_rule, evaluate

import re

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import re
from .models import Rule
from .rule_engine import parse_rule
import logging

logging.basicConfig(level=logging.DEBUG)
import re

import re

def is_valid_rule(rule_string):
    # Check if the rule string is empty
    if not rule_string.strip():
        return "Rule cannot be empty"

    # Check for unbalanced parentheses
    if rule_string.count('(') != rule_string.count(')'):
        return "Unbalanced parentheses"

    # Regular expression to match valid conditions
    condition_pattern = re.compile(r'^\s*([A-Za-z_]+)\s*(=|!=|>|<|>=|<=)\s*([A-Za-z0-9\'"]+)\s*$')

    # Track the last token type
    last_token_type = None  # Can be 'condition', 'operator', or 'parenthesis'
    stack = []  # Stack for balanced parentheses

    # Split the rule into tokens based on logical operators AND/OR
    tokens = re.split(r'(\s+AND\s+|\s+OR\s+|\s*\(\s*|\s*\)\s*)', rule_string)

    for token in tokens:
        token = token.strip()
        if not token:
            continue
        
        # Check for parentheses
        if token == '(':
            stack.append(token)
            last_token_type = 'parenthesis'
            continue
        elif token == ')':
            if not stack:
                return "Unbalanced parentheses"
            stack.pop()
            last_token_type = 'condition'  # Closing a condition
            continue

        # Check if the token is a logical operator
        if token in ['AND', 'OR']:
            # Check for multiple consecutive logical operators or incorrect placement
            if last_token_type in ['operator', None, 'parenthesis']:
                return f"Invalid rule format: Misplaced logical operator '{token}'"
            last_token_type = 'operator'  # Track that the last token was an operator
            continue

        # Validate conditions
        match = condition_pattern.match(token)
        if match:
            attribute, operator, value = match.groups()
            
            # Additional validation for specific attributes
            if attribute == 'department':
                # Ensure the value is a string enclosed in quotes
                if not (value.startswith("'") and value.endswith("'")):
                    return "Department value should be a string enclosed in quotes"
            
            last_token_type = 'condition'  # Mark the last token as a condition
            continue
        
        return f"Invalid condition format: {token}"

    # After processing, check if there are any unmatched parentheses
    if stack:
        return "Unbalanced parentheses"

    # Final check: if the last token was not a condition, that's an error
    if last_token_type != 'condition':
        return "Invalid rule format: Rule cannot end with a logical operator"

    # If all checks are passed
    return None




import logging

@csrf_exempt
def create_rule(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            rule_string = data.get('rule_string', '')

            # Log the received rule string
            logging.debug(f"Received rule string: {rule_string}")

            # Validate the rule
            error = is_valid_rule(rule_string)
            if error:
                logging.debug(f"Rule validation error: {error}")
                return JsonResponse({"error": f"Invalid rule format: {error}"}, status=400)

            # Parse the rule
            ast_root = parse_rule(rule_string)
            logging.debug(f"Parsed AST: {ast_root}")

            # Save the rule to the database
            Rule.objects.create(rule_string=rule_string)

            # Return a success response
            return JsonResponse({"message": "Rule created", "ast": str(ast_root)})

        except json.JSONDecodeError:
            logging.debug("Invalid JSON format in the request body")
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Exception as e:
            logging.error(f"An unexpected error occurred: {str(e)}")
            return JsonResponse({"error": "An unexpected error occurred"}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=400)




@csrf_exempt
def modify_rule(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        rule_id = data.get('rule_id')
        new_rule = data.get('new_rule')

        try:
            # Retrieve the rule from the database
            rule = Rule.objects.get(id=rule_id)
            rule.rule_string = new_rule
            rule.save()

            return JsonResponse({"message": "Rule modified successfully"})
        except Rule.DoesNotExist:
            return JsonResponse({"error": "Rule not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=400)



import logging

@csrf_exempt
def evaluate_rule(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            rule_id = data.get('rule_id')
            user_data = data.get('user_data')

            # Log the received data for debugging
            logging.debug(f"Received data: rule_id={rule_id}, user_data={user_data}")

            # Retrieve the rule from the database
            rule = Rule.objects.get(id=rule_id)
            logging.debug(f"Retrieved rule: {rule.rule_string}")

            # Parse the rule into an Abstract Syntax Tree (AST)
            ast_root = parse_rule(rule.rule_string)
            logging.debug(f"Parsed AST: {ast_root}")

            # Evaluate the rule
            result = evaluate(ast_root, user_data)
            logging.debug(f"Evaluation result: {result}")

            # Return the evaluation result
            return JsonResponse({"result": result})

        except Rule.DoesNotExist:
            logging.error("Rule not found in the database")
            return JsonResponse({"error": "Rule not found"}, status=404)
        except ValueError as ve:
            logging.error(f"ValueError occurred: {str(ve)}")
            return JsonResponse({"error": f"Invalid data: {str(ve)}"}, status=400)
        except json.JSONDecodeError:
            logging.error("Invalid JSON format in the request body")
            return JsonResponse({"error": "Invalid user data format"}, status=400)
        except Exception as e:
            logging.error(f"An unexpected error occurred: {str(e)}")
            return JsonResponse({"error": "An unexpected error occurred"}, status=500)
    else:
        logging.error("Invalid request method")
        return JsonResponse({"error": "Invalid request method"}, status=400)


def index(request):
    return render(request, 'index.html')
