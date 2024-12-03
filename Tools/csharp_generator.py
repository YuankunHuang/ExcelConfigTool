from jinja2 import Template

def generate_csharp_script(class_name: str, fields: dict, output_path: str):
    with open('templates/class_template.cs', 'r') as template_file:
        template = Template(template_file.read())
    content = template.render(class_name=class_name, fields=fields)
    with open(output_path, 'w') as f:
        f.write(content)
