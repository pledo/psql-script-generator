#!/usr/bin/env python3

import argparse
import os
import sys
from jinja2 import Template

def generate_sql_script(app_database, app_readwrite_role, app_user_role, app_user_pass, template_file, output_file):

    # Load Jinja2 template from a file
    template_path = os.path.abspath(os.path.join(os.path.dirname(__file__), template_file))

    if not os.path.exists(template_path):
        # This message works good when running the script from the command line
        #print(error_message.format(template_file, os.getcwd()))
        
        # This message works good when running the script from a container
        error_message = "Error: Template file {}' not found"
        print(error_message.format(template_file))
        exit(1)

    with open(template_path, 'r') as f:
        template = Template(f.read())

    # Render the template    
    rendered_sql_script = template.render(
        app_database=app_database,
        app_readwrite_role=app_readwrite_role,
        app_user_role=app_user_role,
        app_user_pass=app_user_pass,

    )

    # Write the rendered SQL script to the output file
    
    # Error handling, if the output file exists, warn the user and stop the script
    if os.path.exists(output_file):
        error_message = "Error: The output file already exists; please choose another name or delete the existing one: {}" 
        
        # This message works good when running the script from the command line
        #print(error_message.format(os.path.abspath(output_file)))

        # This message works good when running the script from a container
        print(error_message.format(output_file))
        exit(1)
    else:
        output_filename = output_file
        with open(output_filename, 'w') as f:
           f.write(rendered_sql_script)

    print("SQL script generated successfully: {}".format(output_file))    
    
def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Parse command line arguments
    usage_message = "Usage example: python3 generate_sql_script.py -d crawler -w crawler_readwrite_role -u crawler_user -p qweasdzxc -t readwrite_user_template.sql.j2"
    parser = argparse.ArgumentParser(description=usage_message)
    parser.add_argument('-d', '--database', required=True, help='Name of the database')
    parser.add_argument('-w', '--readwrite_role', required=True, help='Name of the readwrite role')
    parser.add_argument('-u', '--user_role', required=True, help='Name of the user role')
    parser.add_argument('-p', '--user_pass', required=True, help='User password')
    parser.add_argument('-t', '--template', required=True, help='Path to the Jinja2 template file')
    parser.add_argument('-o', '--output', required=True, help='Path to the output SQL script file')    
    args = parser.parse_args()

    generate_sql_script(args.database, args.readwrite_role, args.user_role, args.user_pass, args.template, args.output)

if __name__ == '__main__':
    main()