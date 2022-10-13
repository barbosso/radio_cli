import json
from PyInquirer import prompt, Separator
from examples import custom_style_2
from prompt_toolkit.validation import Validator, ValidationError
from pyradios import RadioBrowser
import os


class NumberValidator(Validator):

    def validate(self, document):
        try:
            int(document.text)
        except ValueError:
            raise ValidationError(message="Please enter a number",
                                  cursor_position=len(document.text))


st_dict = {}
st_list = []
# st_txt = []


def get_Radio_Stations():
    rb = RadioBrowser()
    stations = rb.search(countrycode="RU", language="russian")
    count = 0

    for i in stations:
        if "christian" in i["tags"]:
            try:
                stations.remove(i)
            except ValueError:
                pass
        count += 1
        st_name = i["name"]
        st_url = i["url"]
        st_list.append(st_name)
        st_dict.update({st_name: st_url})
        # st_txt.append({"key": count, "stname": st_name, "sturl": st_url})
    # with open('result.json', 'w') as file:
    #     json.dump(st_txt, file, indent=4, ensure_ascii=False)


questions = [{
    'type': 'listwithfilter',
    'name': 'user_option',
    'message': 'Welcome to simple radio-cli',
    'choices': st_list
}]


def main():
    answers = prompt.prompt(questions, style=custom_style_2)
    urlstation = st_dict[answers.get("user_option")]
    print(urlstation)
    os.system(f'mpv --no-video {urlstation} > /dev/null')


if __name__ == "__main__":
    get_Radio_Stations()
    main()
