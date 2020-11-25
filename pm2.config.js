module.exports = {
  apps: [
    {
      name: "socket_server_ssl",
      script: "./main.py",
      watch: true,
      interpreter: "python3",
      interpreter_args: "-u",
    },
  ],
};
