Since fixing this in eclipse is a pain in the ass, but doing it manually makes me hate my existance, we instead use an external python script to autogenerate boring java code.

# "Install"

```
git clone https://github.com/jgsofi/shittyMacro.git
cd shittyMacro
pip install -r requirements.txt
ln -s $PWD/hes.py $HOME/bin/hes
```

# Run

```
hes $( find . -name MyClass.java )
```

Then select the methods you want, and it will append a hashCode and equals function to your class.

# Disclaimer

This is a pile of hacks made quickly without error handling. Commit your code before letting this shitty python stick random snippets into it!