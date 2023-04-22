import sys
import json
import requests
from bs4 import BeautifulSoup


def strip_html_tags(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text()
    text = text.replace('\xa0', ' ')  # 替换非换行空格（NBSP）为普通空格
    return text


def fetch_problem_description(problem_slug, lang='Java'):
    url = 'https://leetcode-cn.com/graphql'
    query = '''
    query questionData($titleSlug: String!) {
        question(titleSlug: $titleSlug) {
            questionId
            questionFrontendId
            translatedTitle
            translatedContent
            codeSnippets {      
                lang      
                langSlug      
                code      
            }
        }
    }
    '''
    variables = {
        'titleSlug': problem_slug
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, json={'query': query, 'variables': variables}, headers=headers)
    if response.status_code != 200:
        print(f'Error: Failed to fetch problem {problem_slug}')
        return None

    data = json.loads(response.text)
    question_data = data['data']['question']
    problem_id = question_data['questionFrontendId']
    problem_title = f"{problem_id}. {question_data['translatedTitle']}"
    problem_description = question_data['translatedContent']
    codeSnippets = question_data['codeSnippets']

    code_snippet = [code for code in codeSnippets if code['lang'] == lang][0]

    # 去除HTML标签
    problem_title = strip_html_tags(problem_title)
    problem_description = strip_html_tags(problem_description)

    return problem_id, problem_title, problem_description, code_snippet


def generate_java_template(problem_slug, file_name, problem_id, problem_title, problem_description, code, method_name):
    problem_class_name = file_name
    java_code = f'''/**
 * {problem_title}
 * <p>
 * {problem_description}
 *
 * 来源：力扣（LeetCode）
 * 链接：https://leetcode-cn.com/problems/{problem_slug}
 */
{code['code']}

'''
    java_code = java_code.replace('Solution', problem_class_name)
    # java_code = java_code.replace(method_name, 'solution')

    return java_code


def pascal_case(s, flag=False):
    ret = ''.join(word.capitalize() for  word in s.split('-'))
    if not flag:
        ret = f'{ret[0].lower()}{ret[1:]}'
    return ret


def main():
    if len(sys.argv) < 3:
        print("Usage: python script.py <argument>")
        sys.exit(1)

    argument = sys.argv[1]
    lang = sys.argv[2]

    print(f"Received argument: {argument}")
    print(f"lang argument: {lang}")

    problem_slug = argument
    question_id, problem_title, problem_description, code_snippet = fetch_problem_description(problem_slug, lang)
    method_name = pascal_case(problem_slug, False)
    file_name = f'_{question_id}_{pascal_case(problem_slug, True)}'

    java_code = generate_java_template(problem_slug, file_name, question_id, problem_title, problem_description, code_snippet, method_name)

    with open(f'{file_name}.java', 'w', encoding='utf-8') as f:
        f.write(java_code)


if __name__ == '__main__':
    main()
