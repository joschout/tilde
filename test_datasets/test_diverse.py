import re

predict1 = 'predict(p(+,+,-,+)).'

predict_regex = r'predict\((.*)\)\.'
predict_pattern = re.compile(predict_regex)

conjunction_regex = r'(\w*)\((.*)\)'
conjunction_pattern = re.compile(conjunction_regex)

argument_regex = '([+-])(\w*)'
argument_pattern = re.compile(argument_regex)


prediction_match = predict_pattern.match(predict1)
if prediction_match is not None:
    prediction_goal = prediction_match.group(1)
    conjunction_match = conjunction_pattern.search(prediction_goal)
    if conjunction_match is not None:
        # TODO: change this from literal to conjunction
        functor = conjunction_match.group(1)
        arguments = conjunction_match.group(2)
        arguments.replace(' ', '')
        arguments = arguments.split(',')
        modes = []
        types = []

        for argument in arguments:
            moded_arg_match = argument_pattern.match(argument)
            if moded_arg_match is not None:
                # mode can only be + or -
                mode = moded_arg_match.group(1)
                type = moded_arg_match.group(2)
                modes.append(mode)
                types.append(type)
            else:
                print('moded_arg not matched')

        print(modes)
        print(types)
    else:
        print('conjunction not matched')
else:
    print('prediction not matched')