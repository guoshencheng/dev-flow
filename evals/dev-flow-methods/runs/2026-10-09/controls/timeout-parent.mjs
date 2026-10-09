import { spawn } from 'node:child_process';
const child = spawn(process.execPath, ['-e', 'require("net").createServer().listen(0,"127.0.0.1",function(){console.log(this.address().port)})'], {stdio:['ignore','pipe','pipe']});
child.stdout.on('data', data => console.log(JSON.stringify({port:Number(data.toString().trim()),pid:child.pid})));
setInterval(() => {}, 1000);
