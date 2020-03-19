// puppeteer
const puppeteer = require('puppeteer');
// csv writting, copied from fast-csv documentation
const fs = require('fs');
//outfile
const outfile = 'email_crawled.csv';

// crawler
(async () => {
    // remove older csv first, and open file writing stream
    try {
        if (fs.exists(outfile)) {
            //file exists, remove it
            fs.unlink(outfile, function (err) {
                if (err) throw err;
                console.log(outfile, ' deleted');
            });
        }
        fs.writeFile(outfile, 'papertitle,author,email,paperlink\n', function (err) {
            if (err) {
                return console.log(err);
            }
            console.log(outfile, ' created');
        });
    } catch (err) {
        console.error(err);
    }

    // lauch browser and open page
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    // 'cmip5' cmip6' search result pages of ametsoc journals
    const paperSearchURLs = [
        'https://journals.ametsoc.org/action/doSearch?AllField=cmip5&pageSize=500&startPage=0',
        'https://journals.ametsoc.org/action/doSearch?AllField=cmip5&pageSize=500&startPage=1',
        'https://journals.ametsoc.org/action/doSearch?AllField=cmip5&pageSize=500&startPage=2',
        'https://journals.ametsoc.org/action/doSearch?AllField=cmip5&pageSize=500&startPage=3',
        'https://journals.ametsoc.org/action/doSearch?AllField=cmip6&pageSize=500&startPage=0',
    ];

    // deal with unhandled promise rejections, or node.js would warned it
    process.on('unhandledRejection', (reason, p) => {
        console.error('Unhandled Rejection at: Promise', p, 'reason:', reason);
        browser.close();
    });

    // loop through search pages
    for (let paperSearchURL of paperSearchURLs) {
        // open search page
        try {
            await page.goto(paperSearchURL);
            console.log('page opened:', paperSearchURL);
        } catch (error) {
            console.log('failed to open:', paperSearchURL);
            console.log(error);
        }

        //getting paper title and link
        let titleSelector = 'a.hlFld-Title';
        await page.waitForSelector(titleSelector);
        let paperTitleLinks = { 'paperTitle': 'N/A', 'paperLink': 'N/A' }
        try {
            paperTitleLinks = await page.$$eval(titleSelector, elements => elements.map(element => {
                return { 'paperTitle': element.innerHTML, 'paperLink': element.href.replace('full', 'abs') }
            }));
        }
        catch (error) {
            console.log(error)
        }

        // for each pair of title and link, get author and email info
        for (let paperTitleLink of paperTitleLinks) {
            try {
                // wait for 4 secs
                await page.waitFor(4000)
                await page.goto(paperTitleLink.paperLink);
                console.log('page opened:', paperTitleLink.paperLink);
            } catch (error) {
                console.log('failed to open:', paperTitleLink.paperLink);
                console.log(error);
            }

            //getting paper author and email
            let authorSelector = 'span.hlFld-ContribAuthor';
            await page.waitForSelector(authorSelector);
            let author = 'N/A'
            try {
                author = await page.$$eval(authorSelector, elements => {
                    element = elements[0];
                    return element.innerHTML;
                });
            }
            catch (error) {
                console.log(error)
            }

            let emailSelector = 'a.email';
            await page.waitForSelector(emailSelector);
            let email = 'N/A'
            try {
                email = await page.$$eval(emailSelector, elements => {
                    element = elements[0];
                    return element.href.replace('mailto:', '');
                });
            }
            catch (error) {
                console.log(error)
            }

            // desired fields of a peper, and append json to local csv file
            paperAbstractInfo = {
                'paperTitle': paperTitleLink.paperTitle,
                'author': author,
                'email': email,
                'paperLink': paperTitleLink.paperLink
            }
            fs.appendFile(outfile, `${paperAbstractInfo.paperTitle},${paperAbstractInfo.author},${paperAbstractInfo.email},${paperAbstractInfo.paperLink}\n`, function (err) {
                if (err) {
                    return console.log(err);
                }
                console.log(outfile, ' append line');
                console.log(paperAbstractInfo);
            });
        }
    }
    await browser.close();
    process.exit()
})();