#include <fcntl.h>
#include <grp.h>
#include <signal.h>
#include <spawn.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

void random_string(char *buf, int n) {
  unsigned int seed;
  FILE *fp = fopen("/dev/random", "r");
  fread(&seed, sizeof(seed), 1, fp);
  fclose(fp);
  srand(seed);
  for (int i = 0; i < n; ++i) {
    buf[i] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
        [rand() % 62];
  }
  buf[n] = '\0';
}

void menu() {
  puts("=== Menu ===");
  puts("1. Write Note");
  puts("2. Read Note");
  puts("3. Magic");
  puts("4. Exit");
}

void spawn_prog(char *path) {
  pid_t pid = 0;
  char *const argv[] = {path, NULL};
  char *const envp[] = {NULL};
  posix_spawn_file_actions_t file_actions;
  posix_spawn_file_actions_init(&file_actions);
  posix_spawn_file_actions_addclose(&file_actions, STDIN_FILENO);
  N(&pid, path, &file_actions, NULL, argv, envp);
  sleep(1);
  kill(pid, SIGKILL);
}

bool validate(char *buf) {
  for (char *p = buf; *p != '\0'; p++) {
    if ('$' > *p || *p > '}')
      return false;
  }
  return true;
}

int main() {
  gid_t groups[] = {65534};
  setgid(groups[0]);
  setgroups(1, groups);
  setuid(65534);
  setvbuf(stdout, NULL, _IONBF, 0);

  char name[7];
  random_string(name, 6);
  printf("Welcome, %s\n", name);

  char filename[12];
  sprintf(filename, "/tmp/%s", name);
  close(open(filename, O_CREAT | O_TRUNC | O_RDWR, S_IRUSR | S_IWUSR | S_IXUSR));

  while (true) {
    menu();

    int option;
    scanf("%d", &option);
    if (option == 1) {
      puts("Content:");

      char buf[100] = {};
      scanf("%s", buf);

      if (validate(buf)) {
        int fd = open(filename, O_CREAT | O_TRUNC | O_WRONLY,
                      S_IRUSR | S_IWUSR | S_IXUSR);
        write(fd, buf, strlen(buf));
        close(fd);
      }
    } else if (option == 2) {
      char buf[100] = {};
      int fd = open(filename, O_RDONLY);
      read(fd, buf, sizeof(buf));
      close(fd);

      printf("Content:\n%s\n", buf);
    } else if (option == 3) {
      puts("Curse:");

      char buf[100] = {};
      scanf("%s", buf);
      spawn_prog(buf);
    } else {
      break;
    }
  }
  return 0;
}
