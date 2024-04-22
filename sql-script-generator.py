#!/usr/bin/env python3

import argparse
import os
import sys
from jinja2 import Template

def generate_sql_script(user_args):

    # Load Jinja2 template from a file
    template_path = os.path.abspath(os.path.join(os.path.dirname(__file__), user_args.template))

    if not os.path.exists(template_path):
        error_message = "Error: Template file {}' not found"
        print(error_message.format(user_args.template, os.getcwd()))
    
        exit(1)

    with open(template_path, 'r') as f:
        template = Template(f.read())

    # Render the template    
    rendered_sql_script = template.render(
        app_database=user_args.database,
        app_readwrite_role=user_args.readwrite_role,
        app_user=user_args.user,
        app_user_pass=user_args.user_pass,

    )

    # Write the rendered SQL script to the output file
    
    # Error handling, if the output file exists, warn the user and stop the script
    if os.path.exists(user_args.output_file):
        error_message = "Error: The output file already exists; please choose another name or delete the existing one: {}"       
        print(error_message.format(os.path.abspath(user_args.output_file)))
        exit(1)

    else:
        output_filename = user_args.output_file
        with open(output_filename, 'w') as f:
           f.write(rendered_sql_script)

    print("SQL script generated successfully: {}".format(user_args.output_file))    
    
def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Parse command line arguments
    usage_message = "Usage example: python3 generate_sql_script.py -d crawler -w crawler_readwrite_role -u crawler_user -p qweasdzxc -t readwrite_user_template.sql.j2"
    parser = argparse.ArgumentParser(description=usage_message)
    parser.add_argument('-d', '--database', required=True, help='Name of the database')
    parser.add_argument('-w', '--readwrite_role', required=True, help='Name of the readwrite role')
    parser.add_argument('-u', '--user', required=True, help='Name of the user')
    parser.add_argument('-p', '--user_pass', required=True, help='User password')
    parser.add_argument('-t', '--template', required=True, help='Path to the Jinja2 template file')
    parser.add_argument('-o', '--output_file', required=True, help='Path of the output SQL script file')    
    args = parser.parse_args()

    class UserArgs:
        def __init__(self, database, readwrite_role, user, user_pass, template, output_file):
            self.database = database
            self.readwrite_role = readwrite_role
            self.user = user
            self.user_pass = user_pass
            self.template = template
            self.output_file = output_file
    
    userargs = UserArgs(args.database, args.readwrite_role, args.user, args.user_pass, args.template, args.output_file)
    
    generate_sql_script(userargs)

if __name__ == '__main__':
    main()