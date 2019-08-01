% This function sets the parameters for reading the VRPN data and opens the
% connection. Run this before executing testSendQuadCmd1_v1.m
% Only needs to be run once.

TrackObj = 2;

% Set Parameters of for reading VRPN data
%==========================================
DeviceName = 'Tracker0@tcp://192.168.0.10'; % Set the name of the trackable and the IP address of the machine streaming the VRPN data
if TrackObj == 2
    DeviceName2 = 'Tracker1@tcp://192.168.0.10'; % Set the name of the trackable and the IP address of the machine streaming the VRPN data
end
timeperiod = 1; % in milliseconds : timeperiod for reading data


if (~exist('trackerInitialized'))
    serverString = DeviceName;
    if TrackObj == 2
        serverString2 = DeviceName2;
    end
    
    timerPeriod = timeperiod;
    
    fprintf(1, 'Adding /media/3CAA4E40AA4DF6C4/vrpn/vrpn/build/java_vrpn to dynamic Java path.\n');
    javaaddpath /media/3CAA4E40AA4DF6C4/vrpn/vrpn/build/java_vrpn;
    
    fprintf(1, 'Adding /media/3CAA4E40AA4DF6C4/vrpn/vrpn/build/java_vrpn/vrpn.jar to dynamic Java path.\n');
    javaaddpath /media/3CAA4E40AA4DF6C4/vrpn/vrpn/build/java_vrpn/vrpn.jar;
    
    % The MyListener constructor can takes up to one parameter:
    % the number of tracker sensors.  When no parameter is
    % specified, it defaults to one sensor.
    fprintf(1, 'Creating position change listener.\n');
    listener = MyListener();
    if TrackObj == 2
        listener2 = MyListener();
    end
    
    % The last four parameters to vrpn.TrackerRemote's constructor
    % are localInLogfileName, localOutLogfileName,
    % remoteInLogfileName, and remoteOutLogfileName.  I have set
    % them to null here by passing the empty matrix.
    fprintf(1, 'Creating tracker.\n');
    tracker = vrpn.TrackerRemote(serverString, [], [], [], []);
    if TrackObj == 2
        tracker2 = vrpn.TrackerRemote(serverString2, [], [], [], []);
    end
    
    % tracker.setTimerPeriod sets how often VRPN's mainloop()
    % function is called, in milliseconds.  I don't know if
    % the default value of 1ms I have set above is too fast,
    % but you can play with the value as needed.
    fprintf(1, 'Setting timerPeriod to %dms.\n', timerPeriod);
    tracker.setTimerPeriod(timerPeriod);
    if TrackObj == 2
        tracker2.setTimerPeriod(timerPeriod);
    end
    
    fprintf(1, 'Adding position change listener to tracker.\n');
    tracker.addPositionChangeListener(listener);
    if TrackObj == 2
        tracker2.addPositionChangeListener(listener2);
    end
    
    trackerInitialized = 1;
end