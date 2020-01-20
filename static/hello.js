window.onload = startInterval;
    function startInterval()
    {
        setInterval("startTime()",1000);
    }

    function startTime()
    {
        window.location.assign("/");
    }
