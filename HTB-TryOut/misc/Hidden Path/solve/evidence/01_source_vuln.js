# Source snippet — challenge/app.js (extracted from misc_hidden_path.zip)
# Note: 'ㅤ' below is U+3164 HANGUL FILLER — an invisible but VALID JS identifier.

app.post('/server_status', async (req, res) => {
    const { choice,ㅤ} = req.body;          // <-- hidden prop 'ㅤ' taken from body
    const integerChoice = +choice;

    if (isNaN(integerChoice)) {
        return res.status(400).send('Invalid choice: must be a number');
    }

    const commands = [
        'free -m',
        'uptime',
        'iostat',
        'mpstat',
        'netstat',
        'ps aux',ㅤ                          // <-- hidden 7th array element = var ㅤ
    ];

    if (integerChoice < 0 || integerChoice >= commands.length) {
        return res.status(400).send('Invalid choice: out of bounds');
    }

    exec(commands[integerChoice], (error, stdout) => { ... });
});

# commands.length == 7  ->  choice=6 passes the bounds check
# commands[6] == ㅤ == req.body['\u3164']  ->  arbitrary command string!
