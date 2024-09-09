# Overview

An example visualization plugin using React and d3. It renders a pie chart on the display pane. Each wedge of the pie corresponds to a signal in the display pane. The size of each wedge is based on the average value of the signal over the display range. 

# Building

A running Seeq Server and an admin access key is a pre-requisite for plugin development. You'll also need You'll need node.js installed globally. 

First run "npm ci" to ensure you've installed the required packages.

Then run "npm run bootstrap" to fetch the latest sdk types and validate the admin credentials. You may be prompted to supply the url to the Seeq server and your access key.

From the example-plugin folder, you can do the following:
 
  **npm run watch**
  
      - watches for code changes and does the following:
        - development webpack build
        - create the plugin
        - uploads the plugin to your Seeq Server

  **npm run build**
  
      - production webpack build
      - create the plugin
      
  **npm run lint**
  
      - runs eslint
      - you can do `npm run lint -- --fix` to automatically fix issues if needed

 # SDK

 Once you've executed "npm run bootstrap", the Seeq plugin API can be referenced at the bottom of the sdk/seeq.d.ts file in the API interface.