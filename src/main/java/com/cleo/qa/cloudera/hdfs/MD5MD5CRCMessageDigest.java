package com.cleo.qa.cloudera.hdfs;

import java.io.IOException;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

import org.apache.hadoop.io.DataOutputBuffer;
import org.apache.hadoop.util.DataChecksum;

public class MD5MD5CRCMessageDigest extends MessageDigest {
    private final int bytesPerChecksum;
    private final int crcsPerBlock;
    private int crcCount;
    private int bytesRead;

    private final byte[] crc = new byte[4];
    private final DataOutputBuffer blockChecksumBuffer;

    private DataOutputBuffer md5DigestBuffer;

    private final DataChecksum checksum;
    private final MessageDigest md5Digest;

    public MD5MD5CRCMessageDigest(String algorithm) throws NoSuchAlgorithmException {
        super(algorithm);

        ChecksumParameters parameters = ChecksumParameters.parseAlgorithm(algorithm);
        this.bytesPerChecksum = parameters.bytesPerChecksum;
        this.crcsPerBlock = parameters.crcsPerBlock;

        md5Digest = MessageDigest.getInstance("MD5");
        blockChecksumBuffer = new DataOutputBuffer();
        md5DigestBuffer = new DataOutputBuffer();
        checksum = DataChecksum.newDataChecksum(parameters.crcType, bytesPerChecksum);
    }

    @Override
    protected byte[] engineDigest() {
        try {
            if (bytesRead > 0)
                flushCrcToBuffer();

            if (blockChecksumBuffer.getLength() > 0)
                calculateMD5OfBlockCrcs();

            md5Digest.update(md5DigestBuffer.getData());
            return md5Digest.digest();

        } catch (final IOException e) {
            throw new RuntimeException(e);
        }
    }

    @Override
    protected void engineReset() {
        blockChecksumBuffer.reset();
        md5DigestBuffer = new DataOutputBuffer();

        checksum.reset();
        md5Digest.reset();

        bytesRead = 0;
        crcCount = 0;
    }

    @Override
    protected void engineUpdate(byte input) {
        checksum.update(input);
        bytesRead += 1;
        try {
            if (bytesRead == bytesPerChecksum)
                flushCrcToBuffer();
        } catch (final IOException e) {
            throw new RuntimeException(e);
        }
    }

    @Override
    protected void engineUpdate(byte[] input, int offset, int len) {
        int bytesRemaining = len;
        final int bytesToComplete = bytesPerChecksum - bytesRead;
        int i = offset;
        try {
            if (bytesRemaining >= bytesToComplete) {
                checksum.update(input, i, bytesToComplete);
                bytesRemaining -= bytesToComplete;
                i += bytesToComplete;
                flushCrcToBuffer();
            }

            while (bytesRemaining >= bytesPerChecksum) {
                checksum.update(input, i, bytesPerChecksum);
                bytesRemaining -= bytesPerChecksum;
                i += bytesPerChecksum;
                flushCrcToBuffer();
            }

            if (bytesRemaining > 0) {
                checksum.update(input, i, bytesRemaining);
                bytesRead += bytesRemaining;
            }

        } catch (final IOException e) {
            throw new RuntimeException(e);
        }
    }

    private void flushCrcToBuffer() throws IOException {
        final int crcLen = checksum.writeValue(crc, 0, true); // true -> resets checksum
        blockChecksumBuffer.write(crc, 0, crcLen);

        bytesRead = 0;
        crcCount += 1;

        if (crcCount == crcsPerBlock)
            calculateMD5OfBlockCrcs();
    }

    private void calculateMD5OfBlockCrcs() throws IOException {
        md5Digest.update(blockChecksumBuffer.getData(), 0, blockChecksumBuffer.getLength());
        md5DigestBuffer.write(md5Digest.digest());
        blockChecksumBuffer.reset();
        md5Digest.reset();
        crcCount = 0;
    }
}
