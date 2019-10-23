#include <iostream>
#include <fstream>
#include "SocketClient.h"

using namespace std;

void onError(errorStruct *e)
{
    cout << e->message << endl;
}

int main()
{
    SocketClient client("192.168.1.240", 8080);
    client.setErrorCallback(onError);
    client.connect();

    string str,tmp;
    string TILT,PAN;


    while(1)
    {
        cout << ">";
        getline(cin, tmp);
        //client.send("TILT:9800");
        cout << "TILT:09800";
        str = "TILT:9800";
        //getline(cin, str);
        client.send(tmp);





    }

    /* NEW */               //  You can now send streams this way

       // The server will receive the STRING CONTENT of the file.
                            // But I'm working on a new version to receive the whole file directly (not as a string)
    /* NEW */

    client.close();
}
