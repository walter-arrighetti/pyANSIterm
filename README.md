# pyANSIterm
Python class to manipulate TTY terminal via ANSI characters, for tweaking with character colors and stylee, cursor positioning, line and screen editing.

It contains a sample code to test the current terminal's graphic capabilities by showing:
 * the standad 16-color palette;
 * the standard indexed-color palette (for terminals `xterm-256color` and above)
 * the standard gray ramp gradient (for terminals `xterm-256color` and above)
 * a subsampling of the full RGB/8 (24 bits/pixel) color cube (for terminals `xterm-24bit` and above)
