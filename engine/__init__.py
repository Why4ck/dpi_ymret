import platform

sys = platform.system()

raw_list = ['goodbyedpi', 'zapret', 'zapret2']
obfs_list = []

print()

if sys == 'Windows':
    obfs_list = raw_list # all tools
if sys == 'Linux':
    obfs_list = [raw_list[2]]