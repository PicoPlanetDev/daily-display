# daily-display

## Overview

Designed to be displayed on a wall-mounted screen, Daily Display combines a today's tasks 
calendar with a pill dispenser and reciept printer to help guide an Alzheimer's disease
patient through their day.

## Source code

The backend relies on Flask, which serves JSON to a Vue frontend using Axios to make requests.

The calendar can be connected to any iCalendar-compatible service, including Google Calendar.
As of right now, the calendar integration can be customized by customizing the auto-generated
`config.ini` file in the `backend` directory with the following contents:

```
# backend/config.ini
calendar_url=yoururlhere
```

In Google Calendar, this URL can be found by hovering over the calendar name in the left navbar,
clicking the menu icon, then clicking *Settings and Sharing*, and scrolling down to the *Integrate calendar*
heading. You can then click the clipboard icon in the *Secret address in iCal format* box, and paste that URL
into the `config.ini` file.