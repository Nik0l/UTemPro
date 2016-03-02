# plotting locations of the users, their communication patterns
library(rworldmap)
library(methods)

dat  = read.csv("locations_so.csv", header = TRUE)
#USERID, LOCATION, LAT1, LON1, ANSWERERID, RESP_TIME, LAT2, LON2
 
#choose line option here
addLines <- 'gc' #'none''straight' 'gc'
if ( addLines == 'gc' ) library(geosphere)

# setting background colours
oceanCol = rgb(7,0,30, maxColorValue=255) 
landCol  = oceanCol 

year <- 2000
for(indNum in 1:2)
{
  users = dat$USERID
  sPDFstack <- joinCountryData2Map(dat, nameJoinColumn='COUNTRY',joinCode='ISO2')
  mapCountryData(sPDFstack, nameColumnToPlot='USERID', mapTitle="World")
  #now plot lines from an asker to answerers
  xAnswerer <- dat$LON2[2]
  yAnswerer <- dat$LAT2[2]
  xAsker    <- dat$LON1
  yAsker    <- dat$LAT1
  respTime  <- dat$RESP_TIME


  ## straight lines
  if ( addLines == 'straight' )
  {
    for(line in 1:length(xAsker))
    {  
       #moving up lower values
       col=rgb(0,1,1,alpha=respTime/500)
       lines(x=c(xAnswerer,xAsker[line]),y=c(yAnswerer,yAsker[line]),col=col, lty="dotted", lwd=0.5)   #lty = "dashed", "dotted", "dotdash", "longdash", lwd some devices support <1
    }
  }
  ## circle lines
  if ( addLines == 'gc')
  {  
    for(line in 1:length(xAsker))
    {
      gC <- gcIntermediate(c(xAnswerer,yAnswerer),c(xAsker[line],yAsker[line]), n=50, breakAtDateLine=TRUE, sp=TRUE)
      col=rgb(0,0,1,alpha=respTime/500)
      lines(gC,col=col,lwd=0.8)
    }
  }  
  #adding coasts in blue looks nice but may distract
  #data(coastsCoarse)
  #plot(coastsCoarse,add=TRUE,col='blue')
  X11(type="cairo") 
  plot(users, ylim = c(30, 70), asp =1)
} 


