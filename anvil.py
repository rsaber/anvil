import sys
import os
import argparse
import yaml
import jinja2
import shutil
import errno

DEFAULT_PROJECT_FILE_NAME = "project.yaml"

class Loader(yaml.SafeLoader):
    def __init__(self, stream):
        self._root = os.path.split(stream.name)[0]
        super(Loader, self).__init__(stream)

    def include(self, node):
        filename = os.path.join(self._root, self.construct_scalar(node))
        with open(filename, 'r') as f:
            return yaml.load(f, Loader)

Loader.add_constructor('!include', Loader.include)

class Project():
    def validate(dictionary):
        if 'pages' not in dictionary:
            return "project requires 'pages' key"
        return None

class Page():
    def validate(dictionary):
        if 'template' not in dictionary:
            return "page requires 'template' key"
        return None

class Anvil:
    def __init__(self, project_directory_path, output_directory_path):
        with open(f'{project_directory_path}/{DEFAULT_PROJECT_FILE_NAME}', 'r') as project:
            project = yaml.load(project, Loader) 
            maybe_error = Project.validate(project)
            if maybe_error is not None:
                print(f'''{arguments.project_path}: error: {maybe_error}''')
                sys.exit(1)

        file_loader = jinja2.FileSystemLoader(f'{project_directory_path}/templates')
        self.environment = jinja2.Environment(loader=file_loader, extensions=['jinja_markdown.MarkdownExtension'])

        self.project_base_path = project_directory_path
        self.output_directory_path = output_directory_path
        self.project = project

        def generate_output_page_path(path):
            filename = path.split('/')[-1]
            filename_without_extension = filename.split('.')[0]
            return f'{filename_without_extension}.html'

        self.page_name_mapping = {}
        for page_path in self.project['pages']:
            self.page_name_mapping[page_path] = generate_output_page_path(page_path)

    def build(self):
        for source in (self.project['copy'] if 'copy' in self.project else []):
            src = f'{self.project_base_path}/{source}'
            dst = f'{self.output_directory_path}/{source}'
            try:
                shutil.copytree(src, dst)
            except OSError as exception:
                if exception.errno in (errno.ENOTDIR, errno.EINVAL):
                    shutil.copy(src, dst)
                else:
                    raise

        for page_path in self.project['pages']:
            self.render_page(page_path)

    def render_page(self, page_path):
        with open(f'{self.project_base_path}/{page_path}', 'r') as raw_page:
            loaded_page = yaml.load(raw_page, Loader)
            maybe_error = Page.validate(loaded_page)
            if maybe_error is not None:
                print(f'''{page_path}: error: {maybe_error}''')
                sys.exit(1)

        template_path = loaded_page['template']
        template = self.environment.get_template(template_path)

        rendered_html = template.render(
            ANVIL_CURRENT_FILENAME=page_path,
            ANVIL_FILENAME_MAPPINGS=self.page_name_mapping,
            **loaded_page
        )
        output_path_to_write_to = self.page_name_mapping[page_path]
        with open(f'{self.output_directory_path}/{output_path_to_write_to}', 'w') as output_file:
            output_file.write(rendered_html)

def main():
    parser = argparse.ArgumentParser(description="A really simple static site generator")
    parser.add_argument("project_path", help="Path to project file")
    parser.add_argument("-o", "--output", help="Output directory")
    arguments = parser.parse_args(sys.argv[1:])

    anvil = Anvil(arguments.project_path, arguments.output) 
    anvil.build()

if __name__ == "__main__":
    main()
