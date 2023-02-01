#include <fcntl.h>
#include <grp.h>
#include <signal.h>
#include <spawn.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int main(){
    pid_t pid = 0;
    char *path = "/bin/sh";
    char *const argv[] = {path, NULL};
    char *const envp[] = {NULL};
    posix_spawn_file_actions_t file_actions;
    posix_spawn_file_actions_init(&file_actions);
    posix_spawn_file_actions_addclose(&file_actions, STDIN_FILENO);
    posix_spawn(&pid, path, &file_actions, NULL, argv, envp);
    sleep(10);
    kill(pid, SIGKILL);
}