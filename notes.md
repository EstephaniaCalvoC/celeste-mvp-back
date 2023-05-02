# Notes

## Dependencies issues

Before install the requirements we need to run

~~~bash
sudo apt-get install python3-setuptools
pip install setuptools
pip install --upgrade setuptools
~~~

~~~txt
 DEPRECATION: html is being installed using the legacy 'setup.py install' method, because it does not have a 'pyproject.toml' and the 'wheel' package is not installed. pip 23.1 will enforce this behaviour change. A possible replacement is to enable the '--use-pep517' option. Discussion can be found at https://github.com/pypa/pip/issues/8559
  Running setup.py install for html ... done
  DEPRECATION: docopt is being installed using the legacy 'setup.py install' method, because it does not have a 'pyproject.toml' and the 'wheel' package is not installed. pip 23.1 will enforce this behaviour change. A possible replacement is to enable the '--use-pep517' option. Discussion can be found at https://github.com/pypa/pip/issues/8559
  Running setup.py install for docopt ... done
 ~~~

 Possible solution:

 This warning message is shown because you are installing a package using an older method that will soon be deprecated by pip¹. The warning message suggests that you enable the '--use-pep517' option as a possible replacement¹. This warning message can be ignored if you are not concerned about future compatibility issues⁴. 

If you want to fix this warning message, you can try enabling the '--use-pep517' option as suggested by pip¹. Alternatively, you can try upgrading pip to version 23.1 or later which will enforce this behavior change¹. 

pip install --use-pep517 <package-name>
