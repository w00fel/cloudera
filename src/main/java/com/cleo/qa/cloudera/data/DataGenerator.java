package com.cleo.qa.cloudera.data;

import java.io.BufferedOutputStream;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.util.Random;

public final class DataGenerator {
    private String path;
    private String size;
    private String name;

    private DataGenerator(String path, String size, String name) {
        this.path = path;
        this.size = size;
        this.name = name;
    }

    public static DataGenerator getInstance(String path, String size, String name) {
        return new DataGenerator(path, size, name);
    }

    public String createTestFile() throws IOException {
        long fileSize = parseSize(size);
        int bufferSize = getBufferSize(size);

        File dataFile = new File(path, name);
        try (OutputStream dataStream = createOutputStream(dataFile, bufferSize)) {
            writeRandomBytes(dataStream, fileSize, new Random());
        }
        return dataFile.getAbsolutePath();
    }

    private static long parseSize(String size) {
        double d = Double.parseDouble(size.replaceAll("[GMK]?B$", ""));
        long l = Math.round(d * 1024 * 1024 * 1024L);
        switch (getSizeModifier(size)) {
            default:  l /= 1024;
            case 'K': l /= 1024;
            case 'M': l /= 1024;
            case 'G': return l;
        }
    }

    private static int getBufferSize(String size) {
        switch (getSizeModifier(size)) {
            default:  return 1024;
            case 'K': return 1024*64;
            case 'M': return 1024*128;
            case 'G': return 1024*512;
        }
    }

    private static char getSizeModifier(String size) {
        int index = Math.max(0, size.length() - 2);
        if (!Character.isLetter(size.charAt(index)))
            index = Math.max(0, size.length() - 1);

        return size.charAt(index);
    }

    private static OutputStream createOutputStream(File output, int bufferSize)
            throws FileNotFoundException {
        return new BufferedOutputStream(new FileOutputStream(output), bufferSize);
    }

    private static void writeRandomBytes(OutputStream stream, long numBytes, Random generator)
            throws IOException {
        int chunkSize = 4096;
        byte[] data = new byte[(int) Math.ceil(chunkSize)];
        long chunks = numBytes / chunkSize;
        long remainder = numBytes % chunkSize;

        for (int i = 0; i < chunks; i++) {
            generator.nextBytes(data);
            stream.write(data);
        }
        stream.write(data, 0, (int) Math.ceil(remainder));
    }
}
