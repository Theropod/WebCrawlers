const puppeteer = require('puppeteer');
(async () => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    const paperSearchURLs = [
        'https://journals.ametsoc.org/action/doSearch?AllField=cmip5&pageSize=10&startPage=0',
        'https://journals.ametsoc.org/action/doSearch?AllField=cmip6&pageSize=10&startPage=0'
    ];

    // deal with unhandled promise rejections, or node.js would warned it
    process.on('unhandledRejection', (reason, p) => {
        console.error('Unhandled Rejection at: Promise', p, 'reason:', reason);
        browser.close();
    });

    for (let paperSearchURL of paperSearchURLs) {
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
        let paperTitleLinks = await page.$$eval(titleSelector, elements => elements.map(element => {
            return { 'paperTitle': element.innerHTML, 'paperLink': element.href }
            }
        ));
        console.log('Got Links:', paperTitleLinks)
    }

    await browser.close();
    process.exit()
})();