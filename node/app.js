const express = require('express');
const app = express();
const port = 3000; // or any port you prefer
const path = require('path');

app.set('view engine', 'ejs');
app.use(express.static(path.join(__dirname, 'public')));

app.get('/', (req, res) => {
    res.render('sell');
});

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
