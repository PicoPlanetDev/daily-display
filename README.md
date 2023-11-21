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
...
calendar_url=yoururlhere
...
```

In Google Calendar, this URL can be found by hovering over the calendar name in the left navbar,
clicking the menu icon, then clicking *Settings and Sharing*, and scrolling down to the *Integrate calendar*
heading. You can then click the clipboard icon in the *Secret address in iCal format* box, and paste that URL
into the `config.ini` file.

## Installation

**Warning:** these steps are incomplete and subject to change. Proceed only with experience!

### Hardware

- Orange Pi Zero 3 (or equivalent) single board computer
  - Alternatives may function with some modifications as well
- PCA9685 PWM driver board
- One servo motor (i.e. Tower Pro SG90) for each type of pill
- Serial thermal printer

### Prerequisites

#### node via nvm

As explained in full detail at [https://github.com/nvm-sh/nvm](https://github.com/nvm-sh/nvm), run the following commands to install node using nvm.
1. Run `curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash` to download and install nvm
2. Close and reopen your terminal
3. Ensure that `command -v nvm` returns `nvm`
4. Install the latest version of node using `nvm install node`

### Set up
1. Install all node modules required for the frontend:
```
cd whiteboard-recorder/frontend
npm install
```
2. Install the Python packages for the backend
```
cd ../backend
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

**To run Daily Display on boot:**
1. Copy `daily-display-backend.service` and `daily-display-frontend.service` into the `/etc/systemd/system` directory
2. Run `sudo systemctl enable daily-display-backend.service` and `sudo systemctl enable daily-display-frontend.service`