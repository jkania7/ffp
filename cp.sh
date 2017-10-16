#!/bin/bash
#created by jwk on 15sep17 to sync files from the obs. date to the psr name folders

rsync -vrah /gbo/AGBT17A_477/*/*_1929+16_*.pfd* /gbo/AGBT17A_477/share/1929+16/
