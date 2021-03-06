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
        'https://journals.ametsoc.org/action/doSearch?AllField=esgf&pageSize=100&startPage=0&sortBy=Ppub',
        'https://journals.ametsoc.org/action/doSearch?AllField=cmip6&pageSize=300&startPage=0&sortBy=Ppub',
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
        let paperTitleLinks = { 'paperTitle': 'N/A', 'paperLink': 'N/A' }
        try {
            await page.waitForSelector(titleSelector);
            paperTitleLinks = await page.$$eval(titleSelector, elements => elements.map(element => {
                // in case paper title includes commas
                return { 'paperTitle': '"' + element.innerHTML + '"', 'paperLink': element.href.replace('full', 'abs') }
            }));
        }
        catch (error) {
            console.log(error)
        }

        // for each pair of title and link, get author and email info
        for (let paperTitleLink of paperTitleLinks) {
            try {
                // wait for 6 secs
                await page.waitFor(6000)
                await page.goto(paperTitleLink.paperLink);
                console.log('page opened:', paperTitleLink.paperLink);
            } catch (error) {
                console.log('failed to open:', paperTitleLink.paperLink);
                console.log(error);
            }

            //getting paper author and email
            let authorSelector = 'span.hlFld-ContribAuthor';
            let author = 'N/A'
            try {
                await page.waitForSelector(authorSelector);
                author = await page.$$eval(authorSelector, elements => {
                    element = elements[0];
                    // in case of commas
                    return '"' + element.innerHTML + '"';
                });
            }
            catch (error) {
                console.log(error)
            }

            let emailSelector = 'a.email';
            let email = 'N/A'
            try {
                await page.waitForSelector(emailSelector);
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