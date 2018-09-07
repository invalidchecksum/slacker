Watches a directory and sends a slack message every 30 seconds if new files have been added

slack token should rest in ~/.slack_token
OR
$SLACK_OAUTH_TOKEN

Works as a daemon in ubuntu with systemctl using the slacker.service file in a systemctl watched directory

Does not actually need to be slack, I just did not want to make it generic.
  sendMsg function can be overwritten with anything you want to run on trigger (i.e. timer expire on interval)
 
