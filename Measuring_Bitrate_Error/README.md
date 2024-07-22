The test TestDistributedH26xBitrateFunctionality is very flaky. This could be caused by either the expected inherent error of the experiment being too large, or there is a bug in the code that needs to be escalated. 

Measurements to Perform: 
- Measure the error of the experiment as a function of time (data points collected). Null hypothesis: If the error is coming from a natural source, we should see this decrease as a function of time in a smooth 1/sqrt(n) curve.  
- Plot a histogram of the errors in this experiment at the current bitrate time. Null hypothesis: If the error is coming from a natural source, this should be a normal distribution without anomalous outliers. 
- Separate the plots for each type of track created. Null hypothesis: If the error is coming from a natural source, all plots should not be statistically significantly different. 
- 






Yuri says:  In most runs, the resulting bitrate is within 10% of the target one but sometimes it’s significantly higher. From the business perspective, an excessive bitrate causes a higher cellular data cost.


