const puppeteer = require('puppeteer');
(async () => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();

    const paperTitleLinks = [{
        paperTitle: 'Atlantic Warm Pool Variability in the CMIP5 Simulations',
        paperLink: 'https://journals.ametsoc.org/doi/abs/10.1175/JCLI-D-12-00556.1'
    },
    {
        paperTitle: 'CMIP5 Projection of Significant Reduction in Extratropical Cyclone Activity over North America',
        paperLink: 'https://journals.ametsoc.org/doi/abs/10.1175/JCLI-D-13-00209.1'
    },
    {
        paperTitle: 'Global and Regional Aspects of Tropical Cyclone Activity in the CMIP5 Models',
        paperLink: 'https://journals.ametsoc.org/doi/abs/10.1175/JCLI-D-12-00549.1'
    },
    {
        paperTitle: 'Simulations of the Eastern North Pacific Intraseasonal Variability in CMIP5 GCMs',
        paperLink: 'https://journals.ametsoc.org/doi/abs/10.1175/JCLI-D-12-00526.1'
    },
    {
        paperTitle: 'MJO and Convectively Coupled Equatorial Waves Simulated by CMIP5 Climate Models',
        paperLink: 'https://journals.ametsoc.org/doi/abs/10.1175/JCLI-D-12-00541.1'
    },
    {
        paperTitle: 'CMIP5 Simulations of Low-Level Tropospheric Temperature and Moisture over the Tropical Americas',
        paperLink: 'https://journals.ametsoc.org/doi/abs/10.1175/JCLI-D-12-00532.1'
    },
    {
        paperTitle: 'North American Climate in CMIP5 Experiments: Part III: Assessment of Twenty-First-Century Projections',
        paperLink: 'https://journals.ametsoc.org/doi/abs/10.1175/JCLI-D-13-00273.1'
    },
    {
        paperTitle: 'CMIP5 Projected Changes in the Annual Cycle of Precipitation in Monsoon Regions',
        paperLink: 'https://journals.ametsoc.org/doi/abs/10.1175/JCLI-D-12-00726.1'
    },
    {
        paperTitle: 'North American Climate in CMIP5 Experiments. Part I: Evaluation of Historical Simulations of Continental and Regional Climatology',
        paperLink: 'https://journals.ametsoc.org/doi/abs/10.1175/JCLI-D-12-00592.1'
    },
    {
        paperTitle: 'ENSO Asymmetry in CMIP5 Models',
        paperLink: 'https://journals.ametsoc.org/doi/abs/10.1175/JCLI-D-13-00454.1'
    }];

    // deal with unhandled promise rejections, or node.js would warned it
    process.on('unhandledRejection', (reason, p) => {
        console.error('Unhandled Rejection at: Promise', p, 'reason:', reason);
        browser.close();
    });

    for (let paperTitleLink of paperTitleLinks) {

        try {
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
                return element.innerHTML;
            });
        }
        catch (error) {
            console.log(error)
        }

        paperabstractInfo = {
            'paperTitle': paperTitleLink.paperTitle,
            'author': author,
            'email': email,
            'paperLink': paperTitleLink.paperLink
        }

        console.log(paperabstractInfo)
    }

    await browser.close();
    process.exit()
})();