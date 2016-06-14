package com.cleo.qa.cloudera.hdfs;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.apache.hadoop.util.DataChecksum;

public class ChecksumParameters {
    public final int bytesPerChecksum;
    public final int crcsPerBlock;
    public final DataChecksum.Type crcType;

    private ChecksumParameters(int bytesPerChecksum, int crcsPerBlock, DataChecksum.Type crcType) {
        this.bytesPerChecksum = bytesPerChecksum;
        this.crcsPerBlock = crcsPerBlock;
        this.crcType = crcType;
    }

    /**
     * Parses an HDFS algorithm string of the form: MD5-of-xxxMD5-of-yyyCRC? where
     *   xxx is crcs per block
     *   yyy is bytes per crc
     *
     * Example: MD5-of-0MD5-of-512CRC32C
     *
     * @param algorithm
     * @return A new instance of this class.
     */
    public static ChecksumParameters parseAlgorithm(String algorithm) {
        String patternString = "MD5-of-(\\d+)MD5-of-(\\d+)(.+$)";
        Pattern pattern = Pattern.compile(patternString);
        Matcher matcher = pattern.matcher(algorithm);

        if (matcher.matches()) {
            int crcsPerBlock = Integer.parseInt(matcher.group(1));
            int bytesPerChecksum = Integer.parseInt(matcher.group(2));
            DataChecksum.Type crcType = DataChecksum.Type.valueOf(matcher.group(3));

            return new ChecksumParameters(bytesPerChecksum, crcsPerBlock, crcType);
        } else {
            throw new IllegalArgumentException(String.format("%s is not a valid algorithm", algorithm));
        }
    }

    @Override
    public String toString() {
        return "ChecksumParameters [bytesPerChecksum=" + bytesPerChecksum +
                ", crcsPerBlock=" + crcsPerBlock + ", crcType=" + crcType + "]";
    }
}
