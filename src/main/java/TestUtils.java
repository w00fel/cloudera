import java.io.BufferedOutputStream;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

import com.cleo.qa.cloudera.data.DataGenerator;
import com.cleo.qa.cloudera.hdfs.MD5MD5CRCMessageDigest;
import com.google.common.io.ByteSource;
import com.google.common.io.ByteStreams;
import com.google.common.io.Files;

public class TestUtils {
    public String createTestFile(String path, String size) throws IOException {
        return createTestFile(path, size, size);
    }

    public String createTestFile(String path, String size, String name) throws IOException {
        return DataGenerator.getInstance(path, size, name).createTestFile();
    }

    public String createTempDirectory() {
        return Files.createTempDir().getAbsolutePath();
    }

    public String appendTestFiles(String directory, String name) throws IOException {
        return appendTestFiles(directory, name, name);
    }

    public String appendTestFiles(String directory, String first, String second) throws IOException {
        String name = String.format("appended.%d", System.currentTimeMillis());
        File file = new File(directory, name);
        ByteSource firstByteSource = Files.asByteSource(new File(first));
        ByteSource secondByteSource = Files.asByteSource(new File(second));

        try (
            OutputStream appendStream = createAppendStream(file);
            InputStream firstStream = firstByteSource.openBufferedStream();
            InputStream secondStream = secondByteSource.openBufferedStream()
        ) {
            ByteStreams.copy(firstStream, appendStream);
            ByteStreams.copy(secondStream, appendStream);
        }
        return file.getAbsolutePath();
    }

    private static OutputStream createAppendStream(File output)
            throws FileNotFoundException {
        return new BufferedOutputStream(new FileOutputStream(output, true));
    }

    public String getChecksum(String fileName, String algorithm) throws NoSuchAlgorithmException, IOException {
        File file = new File(fileName);
        MessageDigest md = new MD5MD5CRCMessageDigest(algorithm);

        return computeMessageDigest(file, md);
    }

    private String computeMessageDigest(File file, MessageDigest md) throws IOException {
        ByteSource byteSource = Files.asByteSource(file);
        try (InputStream stream = byteSource.openBufferedStream()) {
            md.update(ByteStreams.toByteArray(stream));
        }

        return javax.xml.bind.DatatypeConverter.printHexBinary(md.digest()).toLowerCase();
    }

    public String getTimestamp() {
        return String.format("%d", System.currentTimeMillis());
    }

    public String getTimestamp(String suffix) {
        return String.format("%d-%s", System.currentTimeMillis(), suffix);
    }
}
