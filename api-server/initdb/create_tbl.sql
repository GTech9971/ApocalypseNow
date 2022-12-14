/** 的の情報 */
CREATE TABLE target_sites(
    id INT NOT NULL PRIMARY KEY,
    img_path VARCHAR(256),
    hit_img_path VARCHAR(256),
    created_at DATETIME,
    updated_at DATETIME,
    trim_x INT,
    trim_y INT,
    trim_w INT,
    trim_h INT
);

/** 的のヒットポイント */
CREATE TABLE target_site_hit_points(
    target_site_id INT NOT NULL,
    x INT NOT NULL,
    y INT NOT NULL,
    hit_point INT NOT NULL,
    created_at DATETIME,
    FOREIGN KEY (target_site_id) REFERENCES target_sites(id)         
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

/** 未検出画像保存用のテーブル */
CREATE TABLE undetect_target_sites(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    img_path VARCHAR(256) NOT NULL,
    created_at DATETIME
);

/** コマンドのマスタ */
CREATE TABLE command_masters(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    command_desc VARCHAR(256) NOT NULL,
    created_at DATETIME
);

/** ビュワーからのコマンドを記録 */
CREATE TABLE site_commands(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    -- target_site_id INT NOT NULL,                                 サイト未確定の場合の考慮漏れのためコメントアウト
    target_site_id INT NOT NULL,
    command_id INT NOT NULL,
    created_at DATETIME,
    is_done BOOLEAN,
    -- FOREIGN KEY (target_site_id) REFERENCES target_sites(id)     サイト未確定の場合の考慮漏れのためコメントアウト
    --     ON UPDATE CASCADE
    --     ON DELETE CASCADE,
    FOREIGN KEY (command_id) REFERENCES command_masters(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

/** コマンドを追加 */
INSERT INTO command_masters(command_desc, created_at) VALUES
    ('ターゲットサイト画像確定', NOW()),
    ('射撃実行', NOW());