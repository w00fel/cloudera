package com.cleo.qa.cloudera.hdfs;

import java.net.Authenticator;
import java.net.PasswordAuthentication;
import java.net.URL;
import java.net.URLConnection;

public class WebHDFS {
    private String url;
    private String kdc;

    public WebHDFS(String url, String kdc) {
        this.url = url + "/webhdfs/v1/";
        this.kdc = kdc;
    }

    public String authenticate(final String user, final String pass) throws Exception {
        System.setProperty("java.security.krb5.realm", "HADOOP");
        System.setProperty("java.security.krb5.kdc", kdc);

        Authenticator.setDefault(new Authenticator() {
            @Override
            public PasswordAuthentication getPasswordAuthentication() {
                return new PasswordAuthentication(user, pass.toCharArray());
            }
        });

        URLConnection connection = new URL(url).openConnection();

        String headerName=null;
        for (int i = 1; (headerName = connection.getHeaderFieldKey(i)) != null; i++) {
            if (headerName.equals("Set-Cookie")) {
                String cookie = connection.getHeaderField(i);
                String cookieName = cookie.substring(0, cookie.indexOf("="));
                if (cookieName.equals("hadoop.auth")) {
                    return cookie;
                }
            }
        }

        return null;
    }
}
