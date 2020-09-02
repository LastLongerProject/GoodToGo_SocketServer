module.exports = {
    apps: [{
        name: "socket_server",
        script: "./server.py",
        watch: true,
        interpreter: "python3",
        interpreter_args: "-u"
    }]
}
