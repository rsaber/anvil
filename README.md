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
python3 anvil.py my_project_directory --clean --output build
```

Note that `--clean` will remove the contents of the build directory before rebuilding (anything that matches "\*" glob, will exclude ".\*").

Alternatively, Anvil can be set to watch changes in a directory and rebuild entirely upon any file system event.

```
python3 anvil.py my_project_directory --watch --output build
```

## Structure of `project.yaml`

```
>>> project.yaml <<<

# 'buildlist' is a required key 
# indicates the relative path (relative to project directory) of all yaml files to be converted into HTML
buildlist: 
	- my_file_name.yaml

# 'copy' is an optional key
# a list of files/directories to be copied to the output after pages are rendered, used for static data
copy:
	- css
	- fonts
```

## `yaml` page

Each input `yaml` page listed in the `buildlist` key of the `project.yaml` will be rendered into a `html` output. 

```
>>> my_file_name.yaml <<<

# 'template' is a required key
# filename of template to use, all templates must be in my_project_directory/templates
template: base.jinja

# all the keys can be used in the template above during Jinja template generation 
key_one: this is the first value
key_two: this is the second value
```

## Advanced Examples 

As there is no notion of a file tree or website using anvil, only that one yaml file gets built into one html file, we must use non-standard YAML (like !include) to build functional websites. Below is an example illustrating advanced features.

```
>>> Directory Structure <<<

my_advanced_project/
├─ templates/
   ├─ base.jinja
├─ pages/
   ├─ headers.yaml
   ├─ aboutme.yaml
├─ project.yaml 

```

```
>>> headers.yaml <<<
links:
	Home: pages/index.yaml
	About Me: pages/aboutme.yaml
	Resume: pages/resume.yaml
```

```
>>> aboutme.yaml <<< 
template: base.jinja

headers: !include headers.yaml
text: "Hey everyone, this is my about me page!"
```

```
>>> base.jinja <<< 

{% for label, link in headers.links.items() %}
	{% if link == ANVIL_CURRENT_FILENAME %}
		<a class="selected"">{{label}}</a>
	{% else %}
		<a href="{{ ANVIL_FILENAME_MAPPINGS.get(link) }}">{{label}}</a>
	{% endif %}
{% endfor %}
```

##### Kanban

| To Do             | 
|-------------------|
| Add ability to serve static webpages locally, auto refresh on new build | 
| File watcher will build broken web pages and throw exceptions mid build during compilation, keep a backup copy of build during -w | 
| Catch exceptions, and print just the lowest level exception for YAML syntax errors |
| -w mode rebuilds on every file system event, be smarter about this so a rebuild isn't as frequent | 
| Builds with -c or -w clean the entire folder, with non -c or -w keep a hash of files to see what needs to be rebuilt | 
| Add post-processing steps, eg: minify HTML, run bash commands on output files etc |

