module.exports = {
  apps: [
    {
      name: "socket_server",
      script: "./main.py",
      watch: true,
      interpreter: "python3",
      interpreter_args: "-u",
    },
  ],
};
