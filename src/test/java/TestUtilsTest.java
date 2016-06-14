import static org.junit.Assert.assertEquals;

import java.io.File;
import java.net.URL;

import org.junit.Ignore;
import org.junit.Test;

import com.cleo.qa.cloudera.hdfs.ChecksumParameters;

public class TestUtilsTest {
    private static String TMPDIR = System.getProperty("java.io.tmpdir");
    private TestUtils testUtils = new TestUtils();
    private String fileName;
    private File file;

    @Test
    public void test1B() throws Exception {
        fileName = testUtils.createTestFile(TMPDIR, "1B", "spam");
        file = new File(fileName);
        try {
            assertFileLengthEquals(1);
            assertFileNameEquals("spam");
        } finally {
            file.delete();
        }
    }

    @Test
    public void test1KB() throws Exception {
        fileName = testUtils.createTestFile(TMPDIR, "1KB", "eggs");
        file = new File(fileName);
        try {
            assertFileLengthEquals(1024);
            assertFileNameEquals("eggs");
        } finally {
            file.delete();
        }
    }

    @Test
    public void test5P2KB() throws Exception {
        fileName = testUtils.createTestFile(TMPDIR, "5.2KB");
        file = new File(fileName);
        try {
            assertFileLengthEquals(1024*5.2);
            assertFileNameEquals("5.2KB");
        } finally {
            file.delete();
        }
    }

    @Test
    public void test1MB() throws Exception {
        fileName = testUtils.createTestFile(TMPDIR, "1MB");
        file = new File(fileName);
        try {
            assertFileLengthEquals(1024*1024);
            assertFileNameEquals("1MB");
        } finally {
            file.delete();
        }
    }

    @Test
    public void test100P5MB() throws Exception {
        fileName = testUtils.createTestFile(TMPDIR, "100.5MB");
        file = new File(fileName);
        try {
            assertFileLengthEquals(1024*1024*100.5);
            assertFileNameEquals("100.5MB");
        } finally {
            file.delete();
        }
    }

    @Ignore
    public void test1GB() throws Exception {
        fileName = testUtils.createTestFile(TMPDIR, "1GB");
        file = new File(fileName);
        try {
            assertFileLengthEquals(1024*1024*1024);
            assertFileNameEquals("1GB");
        } finally {
            file.delete();
        }
    }

    @Test
    public void testMatcher() {
        String algorithm = "MD5-of-0MD5-of-512CRC32C";
        ChecksumParameters parameters = ChecksumParameters.parseAlgorithm(algorithm);

        assertParametersEqual(0, 512, "CRC32C", parameters);
    }

    @Test(expected = IllegalArgumentException.class)
    public void testMatcherInvalidFormat() {
        String algorithm = "MD2-of-0MD5-of-512CRC32C";
        ChecksumParameters.parseAlgorithm(algorithm);
    }

    @Test(expected = IllegalArgumentException.class)
    public void testMatcherInvalidCRC() {
        String algorithm = "MD5-of-0MD5-of-512SPAM";
        ChecksumParameters.parseAlgorithm(algorithm);
    }

    @Test
    public void testChecksum() throws Exception {
        String expected = "8437ced3acbda21e12240be6509f60ae";
        String fileName = "robotframework/data/bacon.txt";
        String algorithm = "MD5-of-0MD5-of-512CRC32C";

        URL url = ClassLoader.getSystemResource(fileName);
        String actual = testUtils.getChecksum(url.getPath(), algorithm);

        assertEquals(expected, actual);
    }

    private void assertFileLengthEquals(double expectedLength) {
        assertEquals((long) Math.floor(expectedLength), file.length());
    }

    private void assertFileNameEquals(String expectedName) {
        assertEquals(expectedName, file.getName());
    }

    private static void assertParametersEqual(int crcsPerBlock, int bytesPerChecksum,
            String crcType, ChecksumParameters parameters) {
        assertEquals(crcsPerBlock, parameters.crcsPerBlock);
        assertEquals(bytesPerChecksum, parameters.bytesPerChecksum);
        assertEquals(crcType, parameters.crcType.toString());
    }
}
