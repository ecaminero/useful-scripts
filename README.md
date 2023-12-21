# Useful Scripts

In this repository you will find useful commands that helped me with specific problems



### FAQ

- **Doesn't this slow down my shell start up?** Sourcing the file that contains
~500 aliases takes about 30-45 milliseconds in my shell (zsh). I don't think
it's a big deal for me. Measure it with `echo $(($(date +%s%N)/1000000))`
command yourself in your .bashrc/.zshrc.

- **Can I add more Terraform resource types to this?** Please consider forking
  this repo and adding the resource types you want. Not all resource types are
  used by everyone, and adding more resource types slows down shell initialization
  see above).


## Authors

*  **Edwin** - *Initial work* - [github](https://github.com/ecaminero)

## License

This project is licensed under the Apache License - see the [LICENSE.md](LICENSE.md) file for details
