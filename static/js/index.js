window.onload = () => {
    const options = {
        configOverwrite: { toolbarButtons: ['hangup', 'microphone', 'camera'], },
    };

    const api = new JitsiMeetExternalAPI("8x8.vc", {
      roomName: "vpaas-magic-cookie-8bcaab30a250420888f31a7dc45b57b9/{{ room }}",
      // roomName: `vpaas-magic-cookie-8bcaab30a250420888f31a7dc45b57b9/${$("#room").val()}`,
      parentNode: document.querySelector('#jaas-container'),
      configOverwrite: {
        toolbarButtons: ['hangup', 'microphone', 'camera', 'pulse'], 
        customToolbarButtons: [
          {
              icon: 'https://icons.getbootstrap.com/assets/icons/activity.svg',
              // icon: './assets/images/pulse.svg',
              id: 'pulse',
              text: 'Pulse diagnosis'
          }
        ],
      },
    });

    api.addEventListener('toolbarButtonClicked', () => {
      console.log('bbb event');
    });
  }
  