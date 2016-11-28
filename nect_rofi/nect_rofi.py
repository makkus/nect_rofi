# -*- coding: utf-8 -*-

from nect.nect import Nect
from subprocess import PIPE, Popen, check_output

class NectRofi(Nect):

    def nect(self):

        rofi_command = ['rofi']
        rofi_command.append('-dmenu')
        if self.get_config('mesg', False):
            rofi_command.append("-mesg")
            rofi_command.append(self.get_config('mesg'))

        if self.get_config('kb-accept-entry', False):
            rofi_command.append("-kb-accept-entry")
            rofi_command.append(self.get_config('kb-accept-entry'))

        if self.get_config('multi-select', False):
            rofi_command.append('-multi-select')

        if self.get_config('kb-custom', False):

            custom = self.get_config('kb-custom')
            if not type(custom) is dict:
                raise Exception("kb-custom needs to be a dictionary")
            if len(custom) > 19:
                raise Exception("Only up to 19 custom keyboard commands are available")

            i=1
            default_action =  self.get_config('kb-default-action', "default")
            exit_code_map = {0: default_action}

            for k,v in custom.items():
                rofi_command.append("-kb-custom-{}".format(i))
                rofi_command.append(v)
                exit_code_map[i+9] = k
                i=i+1

        if self.get_config('prompt', False):
            prompt = "-p {}".format(self.get_config('prompt'))
            rofi_command.append("-p")
            rofi_command.append(self.get_config('prompt'))

        rofi_proc = Popen(rofi_command, stdout=PIPE, stdin=PIPE, stderr=PIPE)
        for item in self.get_channel():
            rofi_proc.stdin.write("{}\n".format(item).encode())

        outs, errs = rofi_proc.communicate()
        rofi_proc.stdin.close()

        exit_code = rofi_proc.returncode
        exit_command = exit_code_map[exit_code]

        selection = outs.decode().strip()
        selection = selection.split("\n")

        return [{"selection": selection, "command": exit_command}]
