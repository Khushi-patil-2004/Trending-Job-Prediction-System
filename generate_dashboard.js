const ejs = require('ejs');
const fs = require('fs');
const path = require('path');
const csv = require('csv-parser');
const results = [];

// Read the CSV file
fs.createReadStream('data/processed/cleaned_indeed_job_data.csv')
    .pipe(csv())
    .on('data', (row) => results.push(row))
    .on('end', () => {
        // Filter the top 10 job titles for demo purposes
        const topJobs = results.slice(0, 10); // Use your logic to get top jobs

        // Read the EJS template
        ejs.renderFile(path.join(__dirname, 'views', 'job_card.ejs'), { jobs: topJobs }, (err, str) => {
            if (err) {
                console.error('Error rendering EJS template:', err);
                return;
            }

            // Write the output to an HTML file
            fs.writeFileSync('output/dashboard.html', str, 'utf-8');
            console.log('Dashboard HTML saved to output/dashboard.html');
        });
    });
