# anvil 

Using just plain old `yaml` + `jinja2`, anvil aims to be as simple of a static site generator as possible. 

## Quick-start guide 

anvil accepts a project directory file as an input, and an output build directory. The project directory must have the following shape:

```
my_project_directory/
├─ templates/    # where Jinja2 Environment will look for templates
├─ project.yaml  # defining what is to be compiled 

```

```
rm -rf build && mkdir build && python3 anvil.py my_project_directory -o build
```

## Structure of `project.yaml`

```
>>> project.yaml <<<

# 'pages' is a required key 
# indicates the relative path of all yaml files to be converted into HTML
pages: 
	- my_file_name.yaml

# 'copy' is an optional key
# a list of files/directories to be copied to the output after pages are rendered
copy:
  - css
	- fonts
```

## `yaml` page

Each input `yaml` page listed in the `pages` key of the `project.yaml` will be rendered into a `html` output. 

```
>>> my_file_name.yaml <<<

# 'template' is a required key
# filename of template to use, all templates must be in my_project_directory/templates
template: base.jinja

# all the keys can be used in the template above during rendering
key_one: this is the first value
key_two: this is the second value
```

## Advanced Examples 

As there is no notion of a file tree or website using anvil, only that one yaml file gets built into one html file, we must use non-standard YAML (like !include) to build functional websites. 

```
>>> headers.yaml <<<
links:
	Home: pages/index.yaml       # Anvil exports a handy function to convert this filename to the generated output path
	About Me: pages/aboutme.yaml
	Resume: pages/resume.yaml
```

```
>>> aboutme.yaml <<< 
template: base.jinja

headers: !include headers.yaml   # Every yaml page that would have a header would !include this
text: "Hey everyone, this is my about me page!"
```

```
>>> base.jinja <<< 

{% for title, link in headers.links %}
	<a href="{{ anvil_link_for(link) }}">{{title}}</a>
{% endfor %}
```



